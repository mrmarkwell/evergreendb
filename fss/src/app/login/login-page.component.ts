import { Component } from '@angular/core';
import { RestService } from '../rest.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

@Component({
	selector: 'login-page',
    templateUrl: './login-page.component.html',
    styleUrls: ['./login-page.component.scss']
})
export class LoginPage {

    username: string = "";
    password: string = "";
    
    constructor(
        private restService: RestService,
        private router: Router,
        public snackBar: MatSnackBar
    ) {

    }
    
    public attemptLogin() {        
        this.restService.settings.current_username = this.username;
        this.restService.settings.current_password = this.password;
        this.restService.checkLogin().then(success => { 
            if (success) {
                this.router.navigate(['/children'])
            } else {
                this.snackBar.open("Login Failed!", "Close", {
                    duration: 5000,
                  });
            }
        })
    }
}
