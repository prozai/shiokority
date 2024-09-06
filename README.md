# ShiokorityAPI
backend Setup (flask)
<details>
<summary><strong> Windows Users 🪟</strong></summary>

### Clone Our Repository
```bash  
git clone https://github.com/prozai/shiokority.git
```
### ⚙️ Setting up local python environment
#### creating 'env' environment folder  
```bash 
python -m venv env
```
## 🚩 If the environment doesn't activate, check the execution policy:
```bash
Get-ExecutionPolicy
```
## ⚠️ Giving terminal Administrative permission 
Running the following commands with administrative privileges or elevated access can affect your system configuration. Use caution and ensure you understand the implications.
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
## Activating the environment
```bash
env\Scripts\activate
```

### Installing packages
```bash
pip install -r requirements.txt
```
### Deactivate environment
```bash
env\Scripts\deactivate.bat
```

## You can start developing your features!
</details>

<details> 
<summary><strong>macOS/Linux Users 🧑‍💻</strong></summary>

### Clone Our Repository

```bash  
git clone https://github.com/prozai/shiokority.git
```
### ⚙️ Setting up local python environment
## creating 'env' environment folder  
```bash 
python3 -m venv env
```

## Activating the environment
```bash
source env/bin/activate
```

### Installing packages
```bash
pip install -r requirements.txt
```

### Deactivate environment
```bash
deactivate
```
## You can start developing your features!

</details>
<br>

# ShiokorityMerch
Frontend Setup (React)
# ⚠️ Prerequisites
1. Node.js installed

<details>
<summary><strong> Windows Users 🪟</strong></summary>

#### Navigate to the Frontend Directory

1. Change to the frontend directory:
- **Windows Command Prompt**:
     ```bash
     cd frontend
     ```

#### Install the Required Node.js Dependencies
2. Install the necessary Node.js dependencies:
   - **Windows Command Prompt**:
     ```bash
     npm install
     ```

#### Update the React Proxy (If Necessary)
3. Update the React proxy setting if you changed the port in `config.py`. Modify the `proxy` field in `frontend/package.json` to:
   ```json
   "proxy": "http://localhost:5001"

#### Starting the React application
4. **Windows Command Prompt**:
```bash
npm start
```
</details>

<details> 
<summary><strong>macOS/Linux Users 🧑‍💻</strong></summary>

1. Change to the frontend directory:
- **macOS/Linux Bash**:
     ```bash
     cd frontend
     ```

#### Install the Required Node.js Dependencies
2. Install the necessary Node.js dependencies:
   - **macOS/Linux Bash**:
     ```bash
     npm install
     ```

#### Update the React Proxy (If Necessary)
3. Update the React proxy setting if you changed the port in `config.py`. Modify the `proxy` field in `frontend/package.json` to:
   ```json
   "proxy": "http://localhost:5001"

#### Starting the React application
4. **macOS/Linux Bash**:
```bash
npm start
```

</details>