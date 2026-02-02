import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-flats',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './flats.html',
  styleUrl: './flats.css',
})
export class Flats implements OnInit {
  flats: any[] = [];
  filteredFlats: any[] = [];
  filters: {
    swimming_pool: boolean;
    car_parking: boolean;
    bike_parking: boolean;
    gym: boolean;
    garden: boolean;
  } = {
    swimming_pool: false,
    car_parking: false,
    bike_parking: false,
    gym: false,
    garden: false
  };
  maxRent: number = 25000;
  minRent: number = 10000;
  showBookingPopup = false;
  bookingMessage = '';
  showImageModal = false;
  selectedImage = '';

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadFlats();
  }

  loadFlats() {
    this.api.getFlats().subscribe((res: any) => {
      this.flats = res;
      this.filteredFlats = res;
    });
  }

  applyFilters() {
    this.filteredFlats = this.flats.filter(flat => {
      // Rent filter
      if (flat.rent < this.minRent || flat.rent > this.maxRent) {
        return false;
      }
      
      // Amenities filter
      for (let amenity in this.filters) {
        if (this.filters[amenity as keyof typeof this.filters] && !flat.amenities[amenity]) {
          return false;
        }
      }
      
      return true;
    });
  }

  clearFilters() {
    this.filters = {
      swimming_pool: false,
      car_parking: false,
      bike_parking: false,
      gym: false,
      garden: false
    };
    this.maxRent = 25000;
    this.minRent = 10000;
    this.filteredFlats = this.flats;
  }

  bookFlat(flatNo: string) {
    const data = { flat_no: flatNo };
    this.api.bookFlat(data).subscribe((res: any) => {
      this.bookingMessage = 'Booking request sent successfully!';
      this.showBookingPopup = true;
      setTimeout(() => {
        this.showBookingPopup = false;
      }, 3000);
    }, err => {
      this.bookingMessage = 'Please login first!';
      this.showBookingPopup = true;
      setTimeout(() => {
        this.showBookingPopup = false;
        this.router.navigate(['/login']);
      }, 2000);
    });
  }

  closePopup() {
    this.showBookingPopup = false;
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

  goToMyBookings() {
    this.router.navigate(['/my-bookings']);
  }

  viewImage(imageUrl: string) {
    this.selectedImage = 'http://localhost:5000' + imageUrl;
    this.showImageModal = true;
  }

  closeImageModal() {
    this.showImageModal = false;
  }
}
