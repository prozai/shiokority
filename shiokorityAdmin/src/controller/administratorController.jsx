import Administrator from '../model/administrator';

class AdministratorController {
  constructor() {
    this.email = '';
    this.password = '';
    this.status = '';
  }

  setEmail(email) {
    this.email = email;
  }

  setPassword(password) {
    this.password = password;
  }

  setStatus(status) {
    this.status = status;
  }

  async handleLogin(event, navigate) {
    event.preventDefault();
    this.setStatus('Logging in...');
    try {
      
      await Administrator.login(this.email, this.password);
      
      this.setStatus('Login successful');
      navigate('/dashboard');
    } catch (error) {
      this.setStatus('Login failed: ' + error.message);
    }
  }

  async handleLogout(navigate) {
    try {
      await Administrator.logout();
      this.setStatus('Logged out successfully');
      navigate('/login');
    } catch (error) {
      this.setStatus('Logout failed: ' + error.message);
    }
  }

  static isLoggedIn() {
    return Administrator.isLoggedIn();
  }
  
}

export default AdministratorController;