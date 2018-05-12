import { Component, OnInit, OnChanges } from '@angular/core';
import { RestService } from './rest.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MatIconRegistry } from '@angular/material';
import { Router } from '@angular/router';

@Component({
    selector: 'fss-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnChanges {
    title = 'FSS';
    username = "";
    constructor(
        iconRegistry: MatIconRegistry,
        sanitizer: DomSanitizer,
        private router: Router,
        private restService: RestService
    ) {
        iconRegistry.addSvgIcon(
            'refresh_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/refresh_icon.svg'));
        this.username = this.restService.settings.current_username;
    }

    ngOnInit() {
        this.username = this.restService.settings.current_username;        
    }
    ngOnChanges() {
        this.username = this.restService.settings.current_username;
    }
    refresh(): void {
        this.restService.refresh();
    }
    logout(): void {
        this.restService.settings.current_password = "";
        this.restService.settings.current_username = "";
        this.router.navigate(['/login']);
    }
}
