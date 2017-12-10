import { Component, Input, ViewChild, OnChanges, SimpleChanges} from '@angular/core';
import { ParamMap } from '@angular/router';

import { FamilyMember } from '../../family-member';
import { Child } from '../../child';
import { RestService } from '../../rest.service';

import { FamilyListComponent } from './family-list.component';

@Component({
    selector: 'family-info-tab',
    templateUrl: './family-info-tab.component.html',
    styleUrls: ['./family-info-tab.component.scss']
})
export class FamilyTabComponent implements OnChanges {
    constructor(
        private restService: RestService
    ) {}

    ngOnChanges(changes: SimpleChanges): void {
        if ("child_id" in changes) {
            this.family_member = null;
            this.restService.getChild(this.child_id).then(child => this.child = child);
        }
    }

    onSelect(family_member: FamilyMember): void {
        this.family_member = family_member;
    }

    saveFamilyMenber(): void {
        this.restService.updateFamilyMember(this.family_member);
    }

    saveChild(): void {
        this.restService.updateChild(this.child);
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

    family_member: FamilyMember;
    private child: Child;
}
