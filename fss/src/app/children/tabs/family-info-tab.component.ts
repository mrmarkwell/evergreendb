import { Component, OnInit } from '@angular/core';
import { ParamMap } from '@angular/router';

import { FamilyMember } from '../../family-member';
import { RestService } from '../../rest.service';

@Component({
    selector: 'family-info-tab',
    templateUrl: './family-info-tab.component.html',
    styleUrls: ['./family-info-tab.component.css']
})
export class FamilyTabComponent implements OnInit {
    constructor(
        private restService: RestService
    ) {}
    ngOnInit(): void {
    }
		onSelect(family_member: FamilyMember): void {
		  this.family_member = family_member;
			console.log("yay",this.family_member);
		}
    private family_member: FamilyMember;
}
