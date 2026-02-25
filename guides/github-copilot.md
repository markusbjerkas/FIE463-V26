# Installing GitHub Copilot CLI (Command Line Interface)

## Windows

### Installing Node.js

You first need to install Node.js which is a JavaScript runtime required to run GitHub Copilot CLI. 

1. Go to [https://nodejs.org/en/download/](https://nodejs.org/en/download/) to download the installer.
2. **Do not** select the installer versions offered on top, but instead navigate to the line where it says
    *"Or get a prebuilt Node.js® for"* and select `Windows` running on `x64`.
3. Click on the button below which reads `Windows Installer (.msi)` to download the installer.
4. Run the installer and just accept the default options.

### Installing GitHub Copilot CLI

Once you have successfully installed Node.js, you can install [GitHub Copilot CLI](https://github.com/github/copilot-cli).

1. From the Start Menu, launch *Node.js command prompt*.
2. Type the following command to install GitHub Copilot CLI:
    ```cmd
    npm install -g @github/copilot
    ```
3. Copilot CLI should now be installed. You can verify this by typing the following command in the terminal:
    ```cmd
    copilot --version
    ```

## macOS and Linux

1. Open the terminal and run the following command to install GitHub Copilot CLI:
    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```
2. Copilot CLI should now be installed. You can verify this by typing the following command in the terminal:
    ```bash
    copilot --version
    ```
