import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import { catchError } from 'rxjs';
import { environment } from '../../environments/environments';
import { UserInterface } from '../interfaces/user.interface';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButtonModule,
    MatInputModule,
    FormsModule,
    MatCardModule,
    CommonModule,
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
})
export class RegisterComponent {
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  router = inject(Router);
  authService = inject(AuthService);
  registrationForm: FormGroup;
  error: string = '';
  apiUrl: string = environment.apiUrl;
  constructor() {
    this.registrationForm = this.fb.nonNullable.group({
      name: [
        '',
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(30),
        ],
      ],
      email: ['', [Validators.required, Validators.email]],
      password: [
        '',
        [
          Validators.required,
          Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/),
        ],
      ],
    });
  }

  get name() {
    return this.registrationForm.get('name');
  }

  get email() {
    return this.registrationForm.get('email');
  }

  get password() {
    return this.registrationForm.get('password');
  }

  getErrorMessage(controlName: string): string {
    const control = this.registrationForm.get(controlName);
    if (control?.hasError('required')) {
      return 'Field is required';
    }

    if (control?.hasError('email')) {
      return 'Invalid email';
    }

    if (control?.hasError('minlength')) {
      return 'Name must be at least 4 characters.';
    }

    if (control?.hasError('maxlength')) {
      return 'Name must be at most 30 characters.';
    }

    if (control?.hasError('pattern')) {
      return 'Password must include uppercase, lowercase, and numbers, and be at least 8 characters.';
    }

    return '';
  }

  submitForm() {
    if (this.registrationForm.valid) {
      this.http
        .post<{ user: UserInterface }>(
          `${this.apiUrl}/register`,
          {
            name: this.registrationForm.value.name,
            password: this.registrationForm.value.password,
            email: this.registrationForm.value.email,
          },
          { withCredentials: true }
        )
        .pipe(
          catchError((error) => {
            alert(error.error.detail.split(': ')[1]);

            return '';
          })
        )
        .subscribe((response: any) => {
          this.authService.currentUserSig.set(response.user);
          this.authService.accessToken.set(response.accessToken);
          this.router.navigate(['/home']);
        });
    } else {
      this.registrationForm.markAllAsTouched();
    }
  }

  toLogIn() {
    this.router.navigate(['/login']);
  }
}
