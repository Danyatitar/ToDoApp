import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { environment } from '../../environments/environments';
import { HeaderComponent } from '../header/header.component';
import { CategoryInterface } from '../interfaces/category.interface';
import { DialogCategoryAdmin } from '../modals/modal-admin-category';
import { DialogConfirmationDelete } from '../modals/modal-confirmation-delete';

export interface PeriodicElement {
  id: string;
  name: string;
  username?: string;
}

export interface DialogDataCategory {
  category: CategoryInterface;
  isCreate: boolean;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [MatTableModule, CommonModule, MatButtonModule, HeaderComponent],
  templateUrl: './categories.component.html',
  styleUrls: ['./categories.component.css'],
})
export class CategoriesComponent {
  http = inject(HttpClient);
  id?: string;
  apiUrl = environment.apiUrl;
  dialog = inject(MatDialog);
  categories: CategoryInterface[] = [];
  category: CategoryInterface | null = null;
  data: PeriodicElement[] = [];
  displayedColumns: string[] = ['Id', 'name', 'username', 'btn'];
  dataSource = new MatTableDataSource(this.data);

  constructor() {
    this.http
      .get<CategoryInterface[]>(`${this.apiUrl}/category/admin`)
      .subscribe((response) => {
        this.categories = response;
        this.data = response.map((item, index) => {
          return {
            username: item.user?.name,
            name: item.name,
            id: item.id,
          };
        });
        this.dataSource.data = this.data;
      });
  }

  deleteCategory(id: string | undefined) {
    this.category = this.categories.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogConfirmationDelete, {
      data: { description: 'Are you sure you want to delete this category?' },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.http
          .delete(`${this.apiUrl}/category/${id}`)
          .subscribe((response) => {
            this.categories = this.categories.filter((item) => item.id != id);
            this.data = this.categories.map((item, index) => {
              return {
                username: item.user?.name,
                name: item.name,
                id: item.id,
              };
            });
            this.dataSource.data = this.data;
          });
      }
    });
  }

  editCategory(id: string | undefined) {
    this.category = this.categories.filter((item) => item.id == id)[0];
    const dialogRef = this.dialog.open(DialogCategoryAdmin, {
      data: { category: this.category, isCreate: false },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.http
          .patch<CategoryInterface>(`${this.apiUrl}/category/admin/${id}`, {
            name: result.name,
            user_id: result.user_id,
          })
          .subscribe((response) => {
            this.categories = this.categories.map((item) => {
              if (item.id == id) {
                return response;
              }
              return item;
            });

            this.data = this.categories.map((item, index) => {
              return {
                username: item.user?.name,
                name: item.name,
                id: item.id,
              };
            });
            this.dataSource.data = this.data;
          });
      }
    });
  }

  createCategory() {
    this.category = {
      name: '',
      id: '',
    };

    const dialogRef = this.dialog.open(DialogCategoryAdmin, {
      data: { category: this.category, isCreate: true },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.http
          .post<CategoryInterface>(`${this.apiUrl}/category/admin`, {
            name: result.name,
            user_id: result.user_id,
          })
          .subscribe((response) => {
            this.categories.push(response);

            this.data = this.categories.map((item, index) => {
              return {
                username: item.user?.name,
                name: item.name,
                id: item.id,
              };
            });
            this.dataSource.data = this.data;
          });
      }
    });
  }
}
