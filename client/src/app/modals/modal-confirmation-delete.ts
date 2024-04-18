import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
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
import { DialogDataConfirmation } from '../home/home.component';

@Component({
  selector: 'modal-confirmation-delete',
  templateUrl: 'modal-confirmation-delete.html',
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
  styleUrl: '../home/home.component.css',
})
export class DialogConfirmationDelete {
  description = '';
  constructor(
    public dialogRef: MatDialogRef<DialogDataConfirmation>,
    @Inject(MAT_DIALOG_DATA) public data: DialogConfirmationDelete
  ) {
    console.log(data);
    this.description = data.description;
  }

  onNoClick(): void {
    this.dialogRef.close('');
  }
  save() {
    this.dialogRef.close('delete');
  }
}
