import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],   //  THIS IS THE KEY
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  email = '';
  password = '';
  showPassword = false;

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

      // role check (admin / user)
      const payload = JSON.parse(atob(res.token.split('.')[1]));

      if (payload.role === 'admin') {
        this.router.navigate(['/admin-dashboard']);
      } else {
        this.router.navigate(['/flats']);
      }
    }, err => {
      alert('Invalid credentials');
    });
  }
}
