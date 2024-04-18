import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { catchError } from 'rxjs';
import { environment } from '../../environments/environments';
import { HeaderComponent } from '../header/header.component';
import { UserInterface } from '../interfaces/user.interface';
import { DialogConfirmationDelete } from '../modals/modal-confirmation-delete';
import { DialogUser } from '../modals/modal-user';

export interface PeriodicElement {
  name: string;
  position: number;
  email: string;
  id: string;
  role: string;
}

export interface DialogDataUser {
  user: UserInterface;
  isCreate: boolean;
}

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [MatTableModule, CommonModule, MatButtonModule, HeaderComponent],
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css'],
})
export class UsersComponent {
  http = inject(HttpClient);
  id?: string;
  dialog = inject(MatDialog);
  users: UserInterface[] = [];
  user: UserInterface | null = null;
  apiUrl = environment.apiUrl;
  data: PeriodicElement[] = [];
  displayedColumns: string[] = ['Id', 'name', 'email', 'role', 'btn'];
  dataSource = new MatTableDataSource(this.data);

  constructor() {
    this.http
      .get<UserInterface[]>(`${this.apiUrl}/user/admin`)
      .subscribe((response) => {
        this.users = response;
        this.data = response.map((item, index) => {
          return {
            position: index + 1,
            name: item.name,
            email: item.email,
            id: item.id,
            role: item.role,
          };
        });
        this.dataSource.data = this.data;
      });
  }

  deleteUser(id: string | undefined) {
    this.user = this.users.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogConfirmationDelete, {
      data: { description: 'Are you sure you want to delete this user?' },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.http.delete(`${this.apiUrl}/user/${id}`).subscribe((response) => {
          this.users = this.users.filter((item) => item.id != id);
          this.data = this.users.map((item, index) => {
            return {
              position: index + 1,
              name: item.name,
              email: item.email,
              id: item.id,
              role: item.role,
            };
          });
          this.dataSource.data = this.data;
        });
      }
    });
  }

  editUser(id: string | undefined) {
    this.user = this.users.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogUser, {
      data: { user: this.user, isCreate: false },
    });

    dialogRef.afterClosed().subscribe((result: UserInterface) => {
      if (result) {
        this.http
          .patch<UserInterface>(`${this.apiUrl}/user/admin/${id}`, {
            name: result.name,
            email: result.email,
            role: result.role,
          })
          .pipe(
            catchError((error: any) => {
              alert(error.error.detail.split(': ')[1]);

              return '';
            })
          )
          .subscribe((response) => {
            if (!(typeof response == 'string')) {
              this.users = this.users.map((item) => {
                if (item.id == id) {
                  return response;
                }
                return item;
              });
              this.data = this.users.map((item, index) => {
                return {
                  position: index + 1,
                  name: item.name,
                  email: item.email,
                  id: item.id,
                  role: item.role,
                };
              });
              this.dataSource.data = this.data;
            }
          });
      }
    });
  }

  createUser() {
    this.user = {
      id: '',
      accessToken: '',
      name: '',
      password: '',
      email: '',
      role: '',
    };
    const dialogRef = this.dialog.open(DialogUser, {
      data: { user: this.user, isCreate: true },
    });

    dialogRef.afterClosed().subscribe((result: UserInterface) => {
      if (result) {
        this.http
          .post<UserInterface>(`${this.apiUrl}/user/admin`, {
            name: result.name,
            password: result.password,
            email: result.email,
            role: result.role,
          })
          .pipe(
            catchError((error: any) => {
              console.log(error);
              alert(error.error.detail.split(': ')[1]);

              return '';
            })
          )
          .subscribe((response) => {
            if (!(typeof response == 'string')) {
              this.users.push(response);
              this.data = this.users.map((item, index) => {
                return {
                  position: index + 1,
                  name: item.name,
                  email: item.email,
                  id: item.id,
                  role: item.role,
                };
              });
              this.dataSource.data = this.data;
            }
          });
      }
    });
  }
}
