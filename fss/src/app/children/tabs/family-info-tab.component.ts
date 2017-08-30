import { Component, Input, ViewChild } from '@angular/core';
import { ParamMap } from '@angular/router';

import { FamilyMember } from '../../family-member';
import { RestService } from '../../rest.service';

import { FamilyListComponent } from './family-list.component';

@Component({
    selector: 'family-info-tab',
    templateUrl: './family-info-tab.component.html',
    styleUrls: ['./family-info-tab.component.css']
})
export class FamilyTabComponent {
    constructor(
        private restService: RestService
    ) {}
    onSelect(family_member: FamilyMember): void {
      this.family_member = family_member;
    }
    save(): void {
      this.restService.updateFamilyMember(this.family_member);
    }
    delete(): void {
      if (confirm("Are you sure you want to delete this family member?")) {
        this.restService.deleteFamilyMember(this.family_member.id);
        this.family_list.getFamilyMembers();
        this.family_member = null;
      }
    }
    @Input() child_id: number;
    @ViewChild(FamilyListComponent) family_list: FamilyListComponent;
    private family_member: FamilyMember;
}
