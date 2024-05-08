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
import { DialogDataUser } from '../users/users.compnent';

@Component({
  selector: 'modal-user',
  templateUrl: 'modal-user.html',
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
export class DialogUser {
  fb = inject(FormBuilder);
  editForm: FormGroup;
  error = '';
  modalTitle = '';
  http = inject(HttpClient);
  apiUrl: string = environment.apiUrl;

  constructor(
    public dialogRef: MatDialogRef<DialogUser>,
    @Inject(MAT_DIALOG_DATA) public data: DialogDataUser
  ) {
    if (!data.isCreate) {
      this.modalTitle = 'Edit User';
    } else {
      this.modalTitle = 'Create User';
    }

    this.editForm = this.fb.nonNullable.group({
      name: [
        data.user.name,
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(30),
        ],
      ],
      password: [data.user.password, [Validators.minLength(4)]],
      email: [data.user.email, [Validators.required, Validators.email]],
      role: [data.user.role, [Validators.required]],
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
  get password() {
    return this.editForm.get('password');
  }

  get email() {
    return this.editForm.get('email');
  }

  get role() {
    return this.editForm.get('role');
  }

  getErrorMessage(controlName: string): string {
    const control = this.editForm.get(controlName);
    if (control?.hasError('required')) {
      return 'Field is required';
    }

    if (control?.hasError('minlength')) {
      return 'Name must be at least 4 characters.';
    }

    if (control?.hasError('email')) {
      return 'Enter correct email';
    }

    return '';
  }

  save() {
    console.log(this.editForm.valid);
    if (this.editForm.valid) {
      this.data.user.name = this.editForm.value.name;
      this.data.user.email = this.editForm.value.email;
      this.data.user.role = this.editForm.value.role;
      this.data.user.password = this.editForm.value.password;
      console.log(this.data.user);
      this.dialogRef.close(this.data.user);
    }
  }
}
