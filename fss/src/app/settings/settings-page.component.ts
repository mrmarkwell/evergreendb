import { Component } from '@angular/core';
import { RestService } from '../rest.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

@Component({
	selector: 'settings-page',
    templateUrl: './settings-page.component.html',
    styleUrls: ['./settings-page.component.scss']
})
export class SettingsPage {
    
    constructor(
        private restService: RestService,
        private router: Router,
        public snackBar: MatSnackBar
    ) {}

    private dev_mode: boolean = false;

    public onSubmit(): void {
        this.restService.settings.setDevMode(this.dev_mode)
    }

}
