from flask import Flask

app = Flask(__name__)

# Эндпоинт для Lua-скрипта
@app.route('/script.lua', methods=['GET'])
def serve_script():
    lua_script = """
    local player = game.Players.LocalPlayer
    local character = player.Character or player.CharacterAdded:Wait()
    local flying = false
    local flySpeed = 50

    local ScreenGui = Instance.new("ScreenGui", player:WaitForChild("PlayerGui"))
    local flyButton = Instance.new("TextButton")

    -- Настройка кнопки
    flyButton.Size = UDim2.new(0, 200, 0, 100)
    flyButton.Position = UDim2.new(0.5, -100, 0.5, -50)
    flyButton.Text = "Fly"
    flyButton.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
    flyButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    flyButton.Parent = ScreenGui

    local bodyVelocity = Instance.new("BodyVelocity")
    bodyVelocity.Velocity = Vector3.new(0, 0, 0)
    bodyVelocity.MaxForce = Vector3.new(4000, 4000, 4000)

    local function startFlying()
        flying = true
        bodyVelocity.Parent = character.HumanoidRootPart

        while flying do
            local camera = workspace.CurrentCamera
            local direction = camera.CFrame.LookVector
            bodyVelocity.Velocity = (direction * flySpeed) + Vector3.new(0, 20, 0)
            wait(0.1)
        end
        bodyVelocity.Parent = nil
    end

    local function stopFlying()
        flying = false
    end

    -- Обработчик нажатия на кнопку
    flyButton.MouseButton1Click:Connect(function()
        if not flying then
            startFlying()
            flyButton.Text = "Stop Flying"
        else
            stopFlying()
            flyButton.Text = "Fly"
        end
    end)
    """
    return lua_script, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
