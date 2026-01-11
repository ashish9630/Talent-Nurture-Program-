import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  email = '';
  password = '';
  role = 'user';
  showPassword = false;

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
      alert('Registration successful!');
      this.router.navigate(['/login']);
    }, err => {
      alert('Registration failed!');
    });
  }
}
