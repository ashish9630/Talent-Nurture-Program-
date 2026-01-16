import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.css',
})
export class AdminDashboard implements OnInit {
  bookings: any[] = [];
  showPopup = false;
  popupMessage = '';
  popupType = 'success'; // 'success' or 'error'

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadBookings();
  }

  loadBookings() {
    this.api.adminBookings().subscribe((res: any) => {
      this.bookings = res;
    }, err => {
      this.showMessage('Admin access required!', 'error');
      setTimeout(() => {
        this.router.navigate(['/login']);
      }, 2000);
    });
  }

  updateStatus(bookingId: number, status: string) {
    const data = { booking_id: bookingId, status: status };
    this.api.updateStatus(data).subscribe((res: any) => {
      this.showMessage(`Booking ${status} successfully!`, 'success');
      this.loadBookings(); // Reload bookings
    }, err => {
      this.showMessage('Failed to update booking status!', 'error');
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

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
}
