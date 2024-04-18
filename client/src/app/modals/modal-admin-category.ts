import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, Inject, inject } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { environment } from '../../environments/environments';
import { DialogDataCategory } from '../categories/categories.compnent';
import { UserInterface } from '../interfaces/user.interface';

@Component({
  selector: 'modal-admin-category',
  templateUrl: 'modal-admin-category.html',
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
    MatSelectModule,
  ],
  styleUrl: '../home/home.component.css',
})
export class DialogCategoryAdmin {
  fb = inject(FormBuilder);
  editForm: FormGroup;
  error = '';
  modalTitle = '';
  users: UserInterface[] = [];
  http = inject(HttpClient);
  apiUrl: string = environment.apiUrl;

  constructor(
    public dialogRef: MatDialogRef<DialogCategoryAdmin>,
    @Inject(MAT_DIALOG_DATA) public data: DialogDataCategory
  ) {
    this.http
      .get<UserInterface[]>(`${this.apiUrl}/user/admin`)
      .subscribe((response) => {
        if (response.length > 0) {
          this.users = response;
        }
      });

    let u = null;
    if (!data.isCreate) {
      this.modalTitle = 'Edit Task';

      u = data.category.user_id;
    } else {
      this.modalTitle = 'Create Task';
      u = null;
    }

    this.editForm = this.fb.nonNullable.group({
      name: [
        data.category.name,
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(30),
        ],
      ],
      user: [u, [Validators.required]],
    });
  }

  deadlineValidator(control: AbstractControl) {
    const deadlineDate = new Date(control.value);
    const currentDate = new Date();

    if (deadlineDate < currentDate) {
      return { invalidDeadline: true };
    }
    return null;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  get name() {
    return this.editForm.get('name');
  }
  get user() {
    return this.editForm.get('user');
  }

  getErrorMessage(controlName: string): string {
    const control = this.editForm.get(controlName);
    if (control?.hasError('required')) {
      return 'Field is required';
    }

    if (control?.hasError('minlength')) {
      return 'Name must be at least 4 characters.';
    }

    return '';
  }

  save() {
    if (this.editForm.valid) {
      this.data.category.name = this.editForm.value.name;
      this.data.category.user_id = this.editForm.value.user;
      this.dialogRef.close(this.data.category);
    }
  }
}
