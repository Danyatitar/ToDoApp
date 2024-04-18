import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import {
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { environment } from '../../environments/environments';
import { CategoryInterface } from '../interfaces/category.interface';
@Component({
  selector: 'modal-category',
  templateUrl: 'modal-category.html',
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
    ReactiveFormsModule,
  ],
  styleUrl: '../home/home.component.css',
})
export class DialogCategory {
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  categories: CategoryInterface[] = [];
  error = '';
  errorEdit = '';
  id = '';
  hasError = false;
  hasErrorEdit = false;
  modalTitle = '';
  name = '';
  editName = '';
  hasCategories = false;
  isEdit = false;
  apiUrl = environment.apiUrl;

  constructor(public dialogRef: MatDialogRef<any>) {
    this.http
      .get<CategoryInterface[]>(`${this.apiUrl}/category`)
      .subscribe((response) => {
        console.log(response);
        if (response.length > 0) {
          this.hasCategories = true;
          this.categories = response;
        }
      });
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  add() {
    if (!this.name) {
      this.hasError = true;
      this.error = 'Name is required';
    } else if (this.name.length < 4) {
      this.hasError = true;
      this.error = 'Min length is 4 symbols';
    } else {
      this.hasError = false;
      this.http
        .post<CategoryInterface>(`${this.apiUrl}/category`, { name: this.name })
        .subscribe((response) => {
          this.categories.push(response);
          this.name = '';
        });
    }
  }

  delete(id: string) {
    this.http.delete(`${this.apiUrl}/category/${id}`).subscribe((response) => {
      this.categories = this.categories.filter((item) => item.id != id);
    });
  }

  edit(id: string) {
    this.editName = this.categories.filter((item) => item.id == id)[0].name;
    this.isEdit = true;
    this.id = id;
  }

  cancel() {
    this.isEdit = false;
  }

  save() {
    if (!this.editName) {
      this.hasErrorEdit = true;
      this.errorEdit = 'Name is required';
    } else if (this.editName.length < 4) {
      this.hasErrorEdit = true;
      this.errorEdit = 'Min length is 4 symbols';
    } else {
      this.hasErrorEdit = false;
      this.http
        .patch<CategoryInterface>(`${this.apiUrl}/category/${this.id}`, {
          name: this.editName,
        })
        .subscribe((response) => {
          if (response) {
            this.categories.filter((item) => item.id == this.id)[0].name =
              response.name;
            this.isEdit = false;
          }
        });
    }
  }
}
