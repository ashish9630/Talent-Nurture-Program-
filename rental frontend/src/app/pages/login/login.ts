import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  email = '';
  password = '';
  showPassword = false;
  showPopup = false;
  popupMessage = '';
  popupType = 'success';

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  login() {
    const data = {
      email: this.email.trim(),
      password: this.password.trim()
    };

    this.api.login(data).subscribe((res:any) => {
      localStorage.setItem('token', res.token);
      this.showMessage('Login successful!', 'success');

      setTimeout(() => {
        const payload = JSON.parse(atob(res.token.split('.')[1]));
        if (payload.role === 'admin') {
          this.router.navigate(['/admin-dashboard']);
        } else {
          this.router.navigate(['/flats']);
        }
      }, 1500);
    }, err => {
      this.showMessage('Invalid credentials!', 'error');
    });
  }

  showMessage(message: string, type: string) {
    this.popupMessage = message;
    this.popupType = type;
    this.showPopup = true;
    setTimeout(() => {
      this.showPopup = false;
    }, 3000);
  }

  closePopup() {
    this.showPopup = false;
  }
}
