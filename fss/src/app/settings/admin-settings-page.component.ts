import { Component, Inject, OnInit, OnChanges } from '@angular/core';
import { RestService } from '../rest.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA, MatTableDataSource } from '@angular/material';
import {SelectionModel} from '@angular/cdk/collections';

import { User } from '../user'
@Component({
    selector: 'admin-page',
    templateUrl: './admin-settings-page.component.html',
    styleUrls: ['./admin-settings-page.component.scss']
})
export class AdminPage implements OnInit, OnChanges{

    constructor(
        private restService: RestService,
        private router: Router,
        public snackBar: MatSnackBar,
        public dialog: MatDialog
    ) { }

    public onSubmit(): void {
        //this.restService.settings.setDevMode(this.dev_mode)
    }

    public users: MatTableDataSource<User>;
    public current_username = this.restService.settings.current_username;
    columnsToDisplay = ['username', 'is_editor', 'is_admin'];
    selection = new SelectionModel<User>(true, []);
    
    updateUser(user): void {
        this.restService.updateUser(user);
    }
    
    ngOnInit(): void {
        this.restService.getUsers().then(users => this.users = new MatTableDataSource<User>(users));
    }
    
    ngOnChanges(): void {
        this.restService.getUsers().then(users => this.users = new MatTableDataSource<User>(users));
    }

    addUserDialog(): void {
        let dialogRef = this.dialog.open(AddUserDialog, {
            width: '250px'
        });

        dialogRef.afterClosed().subscribe(result => {
            this.ngOnChanges();
        });
    }



}

@Component({
    selector: 'add-user-dialog',
    templateUrl: 'add-user-dialog.html',
    styleUrls: ['./add-user-dialog.scss']
})
export class AddUserDialog {
    user: User = new User();
    confirm_password: string;
    constructor(
        private restService: RestService,
        public snackBar: MatSnackBar,
        public dialogRef: MatDialogRef<AddUserDialog>,
        @Inject(MAT_DIALOG_DATA) public data: any) {

        this.user.is_admin = false;
        this.user.is_editor = false;
    }

    onNoClick(): void {
        this.dialogRef.close();
    }


    public attemptAddUser(): void {
        if (!(this.user.password === this.confirm_password)) {
            this.snackBar.open("Passwords do not match!", "Close", {
                duration: 5000,
            })
        } else {
            this.restService.addUser(this.user).then(success => {
                if (success) {
                    this.snackBar.open(`Successfully added user ${this.user.username}!`, "Close", {
                        duration: 5000,
                    });
                    this.dialogRef.close();

                } else {
                    this.snackBar.open("Failed to add new user!", "Close", {
                        duration: 5000,
                    });
                }
            })
        }
    }
}
