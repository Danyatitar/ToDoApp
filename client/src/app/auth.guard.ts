import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './services/auth.service';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private AuthService: AuthService, private router: Router) {}

  async canActivate(): Promise<boolean> {
    const isTokenExpired = await this.AuthService.isTokenExpired();

    if (isTokenExpired) {
      this.router.navigate(['/login']);
      return false;
    }

    return true;
  }
}
