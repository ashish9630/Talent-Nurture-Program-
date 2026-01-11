import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Register } from './pages/register/register';
import { Flats } from './pages/flats/flats';
import { MyBookings } from './pages/my-bookings/my-bookings';
import { AdminDashboard } from './pages/admin-dashboard/admin-dashboard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: Login
  },
  {
    path: 'register',
    component: Register
  },
  {
    path: 'flats',
    component: Flats
  },
  {
    path: 'my-bookings',
    component: MyBookings
  },
  {
    path: 'admin-dashboard',
    component: AdminDashboard
  }
];
