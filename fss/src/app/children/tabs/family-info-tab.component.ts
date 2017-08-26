import { Component, OnInit } from '@angular/core';
import { ParamMap } from '@angular/router';

import { FamilyMember } from '../../family-member';
import { RestService } from '../../rest.service';

@Component({
    selector: 'family-info-tab',
    templateUrl: './family-info-tab.component.html'
})
export class FamilyTabComponent implements OnInit {
    constructor(
        private restService: RestService
    ) {}
    ngOnInit(): void {
    }
}
