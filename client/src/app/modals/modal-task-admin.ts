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
import { DialogDataTask } from '../home/home.component';
import { CategoryInterface } from '../interfaces/category.interface';
import { UserInterface } from '../interfaces/user.interface';

@Component({
  selector: 'modal-task-admin',
  templateUrl: 'modal-task-admin.html',
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
export class DialogTaskAdmin {
  fb = inject(FormBuilder);
  editForm: FormGroup;
  error = '';
  modalTitle = '';
  http = inject(HttpClient);
  categories: CategoryInterface[] = [];
  users: UserInterface[] = [];
  apiUrl: string = environment.apiUrl;

  constructor(
    public dialogRef: MatDialogRef<DialogTaskAdmin>,
    @Inject(MAT_DIALOG_DATA) public data: DialogDataTask
  ) {
    this.http
      .get<CategoryInterface[]>(`${this.apiUrl}/category/admin`)
      .subscribe((response) => {
        if (response.length > 0) {
          this.categories = response.filter(
            (item) => item.user_id === data.task.user_id
          );
        }
      });
    this.http
      .get<UserInterface[]>(`${this.apiUrl}/user/admin`)
      .subscribe((response) => {
        if (response.length > 0) {
          this.users = response;
        }
      });
    let c;
    if (!data.isCreate) {
      this.modalTitle = 'Edit Task';
      if (!data.task.category_id) {
        c = 0;
      } else {
        c = data.task.category_id;
      }
    } else {
      this.modalTitle = 'Create Task';
      c = 0;
    }

    let u = null;
    if (!data.isCreate) {
      this.modalTitle = 'Edit Task';

      u = data.task.user_id;
    } else {
      this.modalTitle = 'Create Task';
      u = null;
    }

    this.editForm = this.fb.nonNullable.group({
      title: [
        data.task.title,
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(30),
        ],
      ],
      description: [data.task.description, [Validators.required]],
      deadline: [
        data.task.deadline,
        [Validators.required, this.deadlineValidator],
      ],
      status: [data.task.status, [Validators.required]],
      category: [c, [Validators.required]],
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

  get title() {
    return this.editForm.get('title');
  }

  get description() {
    return this.editForm.get('description');
  }

  get deadline() {
    return this.editForm.get('deadline');
  }

  getErrorMessage(controlName: string): string {
    const control = this.editForm.get(controlName);
    if (control?.hasError('required')) {
      return 'Field is required';
    }

    if (control?.hasError('minlength')) {
      return 'Name must be at least 4 characters.';
    }

    if (control?.hasError('invalidDeadline')) {
      return "Deadline must be later than or equal to today's date.";
    }

    return '';
  }

  changeCategories(event: any) {
    this.http
      .get<CategoryInterface[]>(`${this.apiUrl}/category/admin`)
      .subscribe((response) => {
        if (response.length > 0) {
          this.categories = response.filter(
            (item) => item.user_id === event.value
          );
        }
        this.editForm.value.category = 0;
      });
  }

  save() {
    if (this.editForm.valid) {
      this.data.task.title = this.editForm.value.title;
      this.data.task.description = this.editForm.value.description;
      this.data.task.deadline = this.editForm.value.deadline;
      this.data.task.status = this.editForm.value.status;

      if (!this.editForm.value.category) {
        this.data.task.category_id = null;
      } else {
        this.data.task.category_id = this.editForm.value.category;
      }

      this.data.task.user_id = this.editForm.value.user;
      this.dialogRef.close(this.data.task);
    }
  }
}
