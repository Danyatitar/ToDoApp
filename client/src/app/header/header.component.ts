import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, Inject, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';
import { Router } from '@angular/router';
import { environment } from '../../environments/environments';
import { UserInterface } from '../interfaces/user.interface';
import { AuthService } from './../services/auth.service';

export interface DialogData {
  name: string;
}

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatMenuModule,
    FormsModule,
    MatInputModule,
    MatFormFieldModule,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
})
export class HeaderComponent {
  name: string = '';

  dialog = inject(MatDialog);
  http = inject(HttpClient);
  apiUrl: string = environment.apiUrl;
  AuthService = inject(AuthService);
  router = inject(Router);
  userName: string | null | undefined = '';
  isAdmin = this.AuthService.currentUserSig()?.role === 'admin';

  constructor() {
    if (!this.AuthService.currentUserSig()) {
      this.http
        .get<UserInterface>(`${this.apiUrl}/user`)
        .subscribe((response) => {
          this.AuthService.currentUserSig.set(response);
          this.isAdmin = response.role === 'admin';
          this.userName = response.name;
        });
    } else {
      this.userName = this.AuthService.currentUserSig()?.name;
    }
  }

  async logOut() {
    this.http
      .post(
        `${this.apiUrl}/logout`,
        {},
        {
          withCredentials: true,
        }
      )
      .subscribe((response) => {
        this.router.navigate(['login']);
        this.AuthService.accessToken.set('');
        this.AuthService.currentUserSig.set(null);
      });
  }

  changeName() {
    const dialogRef = this.dialog.open(Dialog, {
      data: { name: this.name },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.userName = result;
        this.http
          .patch<UserInterface>(`${this.apiUrl}/user`, {
            name: this.userName,
          })
          .subscribe((response) => {
            this.AuthService.currentUserSig.set(response);
          });
      }
    });
  }

  toUsers() {
    this.router.navigate(['/users']);
  }
  toCategories() {
    this.router.navigate(['/categories']);
  }
  toTasks() {
    this.router.navigate(['/tasks']);
  }
}

@Component({
  selector: 'modal-header',
  templateUrl: 'modal-header.html',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
    CommonModule,
  ],
  styleUrl: './header.component.css',
})
export class Dialog {
  hasError = false;
  error = '';
  router = inject(Router);
  AuthService = inject(AuthService);
  constructor(
    public dialogRef: MatDialogRef<Dialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {
    data.name = String(this.AuthService.currentUserSig()?.name);
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  save() {
    if (!this.data.name) {
      this.hasError = true;
      this.error = 'Name is required';
    } else if (this.data.name.length < 4) {
      this.hasError = true;
      this.error = 'Min length is 4 symbols';
    } else {
      this.hasError = false;
      this.dialogRef.close(this.data.name);
    }
  }
}
