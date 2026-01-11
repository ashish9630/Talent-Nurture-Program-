import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://127.0.0.1:8081';

  constructor(private http: HttpClient) {}

  getHeaders() {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      })
    };
  }

  login(data:any) {
    return this.http.post(`${this.baseUrl}/login`, data);
  }

  register(data:any) {
    return this.http.post(`${this.baseUrl}/register`, data);
  }

  getFlats() {
    return this.http.get(`${this.baseUrl}/flats`);
  }

  bookFlat(data:any) {
    return this.http.post(`${this.baseUrl}/book-flat`, data, this.getHeaders());
  }

  myBookings() {
    return this.http.get(`${this.baseUrl}/my-bookings`, this.getHeaders());
  }

  adminBookings() {
    return this.http.get(`${this.baseUrl}/admin/bookings`, this.getHeaders());
  }

  updateStatus(data:any) {
    return this.http.post(`${this.baseUrl}/admin/update-status`, data, this.getHeaders());
  }
}
