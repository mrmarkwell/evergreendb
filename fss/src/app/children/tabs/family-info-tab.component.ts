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
        this.restService.getFamilyMembers(1).then(family_members => { console.log(family_members); this.family_members =  family_members });
    }
    private family_members: FamilyMember[];
}