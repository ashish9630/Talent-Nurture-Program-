import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  email = '';
  password = '';
  role = 'user';
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

  register() {
    const data = {
      email: this.email.trim(),
      password: this.password.trim(),
      role: this.role.trim()
    };

    this.api.register(data).subscribe((res: any) => {
      this.showMessage('Registration successful!', 'success');
      setTimeout(() => {
        this.router.navigate(['/login']);
      }, 2000);
    }, err => {
      this.showMessage('Registration failed!', 'error');
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
