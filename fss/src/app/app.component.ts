import { Component } from '@angular/core';
import { RestService } from './rest.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MatIconRegistry } from '@angular/material';

@Component({
    selector: 'fss-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'FSS';

    constructor(
        iconRegistry: MatIconRegistry,
        sanitizer: DomSanitizer,
        private restService: RestService
    ) {
        iconRegistry.addSvgIcon(
            'refresh_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/refresh_icon.svg'));
    }

    refresh(): void {
        this.restService.refresh();
    }
}
