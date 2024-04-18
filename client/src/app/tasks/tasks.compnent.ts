import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { environment } from '../../environments/environments';
import { HeaderComponent } from '../header/header.component';
import { Status, TaskInterface } from '../interfaces/task.interface';
import { DialogConfirmationDelete } from '../modals/modal-confirmation-delete';
import { DialogTaskAdmin } from '../modals/modal-task-admin';

interface PeriodicElement {
  Id?: string;
  title: string;
  deadline: Date;
  status: Status;
  categoryName?: string;
  username?: string;
}

@Component({
  selector: 'app-tasks',
  standalone: true,
  imports: [MatTableModule, CommonModule, MatButtonModule, HeaderComponent],
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css'],
})
export class TasksComponent {
  http = inject(HttpClient);
  id?: string;
  dialog = inject(MatDialog);
  task: TaskInterface | null = null;
  tasks: TaskInterface[] = [];
  apiUrl = environment.apiUrl;
  data: PeriodicElement[] = [];
  displayedColumns: string[] = [
    'Id',
    'title',
    'deadline',
    'status',
    'categoryName',
    'username',
    'btn',
  ];
  dataSource = new MatTableDataSource(this.data);

  constructor() {
    this.http
      .get<TaskInterface[]>(`${this.apiUrl}/tasks/admin`)
      .subscribe((response) => {
        this.tasks = response;
        this.data = response.map((item, index) => {
          return {
            Id: item.id,
            title: item.title,
            deadline: item.deadline,
            status: item.status,
            categoryName: item.category?.name,
            username: item.user?.name,
          };
        });
        this.dataSource.data = this.data;
      });
  }

  editTask(id: string | undefined) {
    this.task = this.tasks.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogTaskAdmin, {
      data: { task: this.task, isCreate: false },
    });

    dialogRef.afterClosed().subscribe((result: TaskInterface) => {
      if (result) {
        console.log(result);
        this.http
          .put<TaskInterface>(`${this.apiUrl}/tasks/admin/${id}`, {
            title: result.title,
            description: result.description,
            deadline: result.deadline,
            status: result.status,
            category_id: result.category_id,
            user_id: result.user_id,
          })
          .subscribe((response) => {
            console.log(response);
            this.tasks = this.tasks.map((item) => {
              if (item.id == id) {
                return response;
              }
              return item;
            });

            this.data = this.tasks.map((item) => {
              return {
                Id: item.id,
                title: item.title,
                deadline: item.deadline,
                status: item.status,
                categoryName: item.category?.name,
                username: item.user?.name,
              };
            });
            this.dataSource.data = this.data;
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

          this.data = this.tasks.map((item) => {
            return {
              Id: item.id,
              title: item.title,
              deadline: item.deadline,
              status: item.status,
              categoryName: item.category?.name,
              username: item.user?.name,
            };
          });
          this.dataSource.data = this.data;
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
    const dialogRef = this.dialog.open(DialogTaskAdmin, {
      data: { task: this.task, isCreate: true },
    });

    dialogRef.afterClosed().subscribe((result: TaskInterface) => {
      if (result) {
        this.http
          .post<TaskInterface>(`${this.apiUrl}/tasks/admin`, {
            title: result.title,
            description: result.description,
            deadline: result.deadline,
            status: result.status,
            category_id: result.category_id,
            user_id: result.user_id,
          })
          .subscribe((response) => {
            this.tasks.push(response);
            this.data = this.tasks.map((item) => {
              return {
                Id: item.id,
                title: item.title,
                deadline: item.deadline,
                status: item.status,
                categoryName: item.category?.name,
                username: item.user?.name,
              };
            });
            this.dataSource.data = this.data;
          });
      }
    });
  }
}
