import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, effect, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { catchError } from 'rxjs';
import { environment } from '../../environments/environments';
import { HeaderComponent } from '../header/header.component';
import { CategoryInterface } from '../interfaces/category.interface';
import { Status, TaskInterface } from '../interfaces/task.interface';
import { UserInterface } from '../interfaces/user.interface';
import { DialogCategory } from '../modals/modal-category';
import { DialogConfirmationDelete } from '../modals/modal-confirmation-delete';
import { DialogTask } from '../modals/modal-task';
import { AuthService } from '../services/auth.service';

export interface DialogDataTask {
  task: TaskInterface;
  isCreate: boolean;
}

export interface DialogDataConfirmation {
  description: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, HeaderComponent, MatButtonModule, MatCardModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent implements OnInit {
  http = inject(HttpClient);
  router = inject(Router);
  dialog = inject(MatDialog);
  apiUrl: string = environment.apiUrl;
  tasks: TaskInterface[] = [];
  hasTasks: boolean = false;
  task: TaskInterface | null = null;
  AuthService = inject(AuthService);
  categories: CategoryInterface[] = [];

  handleIsAdmin = effect(() => {
    if (this.AuthService.currentUserSig()?.role === 'admin') {
      this.router.navigate(['users']);
    }
  });

  ngOnInit(): void {
    this.http
      .get<UserInterface>(`${this.apiUrl}/tasks`)
      .pipe(
        catchError((error) => {
          console.log(error);
          return '';
        })
      )
      .subscribe((response: any) => {
        this.tasks = response;
        if (this.tasks.length > 0) {
          this.hasTasks = true;
        } else {
          this.hasTasks = false;
        }
      });
  }

  editTask(id: string | undefined) {
    this.task = this.tasks.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogTask, {
      data: { task: this.task, isCreate: false },
    });

    dialogRef.afterClosed().subscribe((result: TaskInterface) => {
      if (result) {
        this.http
          .put<TaskInterface>(`${this.apiUrl}/tasks/${id}`, {
            title: result.title,
            description: result.description,
            deadline: result.deadline,
            status: result.status,
            category_id: result.category_id,
          })
          .subscribe((response) => {
            console.log(response);
            this.tasks = this.tasks.map((item) => {
              if (item.id == id) {
                return response;
              }
              return item;
            });
          });
      }
    });
  }
  createTask() {
    this.task = {
      title: '',
      description: '',
      deadline: new Date(),
      status: Status.Waiting,
    };
    const dialogRef = this.dialog.open(DialogTask, {
      data: { task: this.task, isCreate: true },
    });

    dialogRef.afterClosed().subscribe((result: TaskInterface) => {
      if (result) {
        this.http
          .post<TaskInterface>(`${this.apiUrl}/tasks`, {
            title: result.title,
            description: result.description,
            deadline: result.deadline,
            status: result.status,
            category_id: result.category_id,
          })
          .subscribe((response) => {
            this.tasks.push(response);
          });
      }
    });
  }

  deleteTask(id: string | undefined) {
    this.task = this.tasks.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogConfirmationDelete, {
      data: { description: 'Are you sure you want to delete this task?' },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.http.delete(`${this.apiUrl}/tasks/${id}`).subscribe((response) => {
          this.tasks = this.tasks.filter((item) => item.id != id);
        });
      }
    });
  }

  openCategories() {
    const dialogRef = this.dialog.open(DialogCategory);
    dialogRef.afterClosed().subscribe((result) => {
      this.http
        .get<UserInterface>(`${this.apiUrl}/tasks`)
        .pipe(
          catchError((error) => {
            console.log(error);
            return '';
          })
        )
        .subscribe((response: any) => {
          this.tasks = response;
          if (this.tasks.length > 0) {
            this.hasTasks = true;
          } else {
            this.hasTasks = false;
          }
        });
    });
  }
}
