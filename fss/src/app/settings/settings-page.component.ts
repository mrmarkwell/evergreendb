import { Component, Inject } from '@angular/core';
import { RestService } from '../rest.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

@Component({
    selector: 'settings-page',
    templateUrl: './settings-page.component.html',
    styleUrls: ['./settings-page.component.scss']
})
export class SettingsPage {

    constructor(
        private restService: RestService,
        private router: Router,
        public snackBar: MatSnackBar,
        public dialog: MatDialog
    ) { }

    dev_mode: boolean = !this.restService.settings.evergreen_url.includes("matthewmarkwell");

    public onSubmit(): void {
        this.restService.settings.setDevMode(this.dev_mode)
    }

    openPasswordDialog(): void {
        let dialogRef = this.dialog.open(PasswordChangeDialog, {
            width: '250px'
            //data: { name: this.name, animal: this.animal }
        });

        dialogRef.afterClosed().subscribe(result => {
            console.log('The dialog was closed');
            //this.animal = result;
        });
    }



}

@Component({
    selector: 'password-change-dialog',
    templateUrl: 'password-change-dialog.html',
    styleUrls: ['./password-change-dialog.scss']
})
export class PasswordChangeDialog {

    constructor(
        private restService: RestService,
        public snackBar: MatSnackBar,
        public dialogRef: MatDialogRef<PasswordChangeDialog>,
        @Inject(MAT_DIALOG_DATA) public data: any) { }

    onNoClick(): void {
        this.dialogRef.close();
    }

    old_password: string;
    first_password: string;
    second_password: string;

    public attemptPasswordChange(): void {
        this.restService.checkLogin(this.old_password).then(success => {
            if (success) {
                if (this.first_password === this.second_password) {
                    this.restService.changePassword(this.first_password).then(success => {
                        if (success) {
                            this.snackBar.open("Successfully changed password!", "Close", {
                                duration: 5000,
                              });
                              this.dialogRef.close();
                        } else {
                            this.snackBar.open("Failed to change password!", "Close", {
                                duration: 5000,
                              });
                        }
                    })

                } else {
                    this.snackBar.open("Passwords do not match!", "Close", {
                        duration: 5000,
                      });
                }

            } else {
                this.snackBar.open("Old Password is incorrect!", "Close", {
                    duration: 5000,
                  });
            }
        })
    }
}
