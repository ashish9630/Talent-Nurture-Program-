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
      alert('Admin access required!');
      this.router.navigate(['/login']);
    });
  }

  updateStatus(bookingId: number, status: string) {
    const data = { booking_id: bookingId, status: status };
    this.api.updateStatus(data).subscribe((res: any) => {
      alert(`Booking ${status}!`);
      this.loadBookings(); // Reload bookings
    });
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
}
