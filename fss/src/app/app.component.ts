import { Component } from '@angular/core';
import { RestService } from './rest.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MdIconRegistry } from '@angular/material';

@Component({
    selector: 'fss-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'FSS';

    constructor(
        iconRegistry: MdIconRegistry,
        sanitizer: DomSanitizer,
        private restService: RestService
    ) {
        iconRegistry.addSvgIcon(
            'refresh_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/refresh_icon.svg'));
    }

    refresh(): void {
        this.restService.changeEmitter.emit();
    }
}
