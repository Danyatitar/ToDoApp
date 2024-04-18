import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import { environment } from '../../environments/environments';

import { catchError } from 'rxjs';
import { UserInterface } from '../interfaces/user.interface';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButtonModule,
    MatInputModule,
    FormsModule,
    MatCardModule,
    CommonModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  router = inject(Router);
  authService = inject(AuthService);
  loginForm: FormGroup;
  error: string = '';
  apiUrl: string = environment.apiUrl;

  constructor() {
    this.loginForm = this.fb.nonNullable.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  get email() {
    return this.loginForm.get('email');
  }

  get password() {
    return this.loginForm.get('password');
  }

  getErrorMessage(controlName: string): string {
    const control = this.loginForm.get(controlName);
    if (control?.hasError('required')) {
      return 'Field is required';
    }

    if (control?.hasError('email')) {
      return 'Invalid email';
    }

    return '';
  }

  submitForm() {
    if (this.loginForm.valid) {
      this.http
        .post<{ user: UserInterface }>(
          `${this.apiUrl}/login`,
          {
            password: this.loginForm.value.password,
            email: this.loginForm.value.email,
          },
          { withCredentials: true }
        )
        .pipe(
          catchError((error) => {
            console.log(error);
            this.error = error.error.detail.split(': ')[1];
            return '';
          })
        )
        .subscribe((response: any) => {
          this.error = '';
          // this.authService.currentUserSig.set(response.user);
          this.authService.accessToken.set(response.access_token);
          this.router.navigate(['/home']);
        });
    } else {
      this.loginForm.markAllAsTouched();
    }
  }

  toRegister() {
    this.router.navigate(['/register']);
  }
}
