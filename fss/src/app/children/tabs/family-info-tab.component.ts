import { Component, Input, ViewChild, OnChanges, OnInit, SimpleChanges} from '@angular/core';
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
export class FamilyTabComponent implements OnInit, OnChanges {
    constructor(
        private restService: RestService
    ) {}

    ngOnInit(): void {
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges({} as SimpleChanges));
        setInterval(()=>this.autosave(), this.restService.settings.save_notify_interval);
    }

    ngOnChanges(changes: SimpleChanges): void {
        this.getChild();
        if ("child_id" in changes) {
            this.family_member = null;
        }
    }

    getChild(): void {
        this.restService.getChild(this.child_id).then(child => {
            this.child = child;
        });
    }

    onSelect(family_member: FamilyMember): void {
        this.setFamilyMember(family_member);
    }

    setFamilyMember(family_member: FamilyMember): void {
      this.family_member = family_member;
      this.orig_family_member = Object.assign(Object.create(family_member), family_member); // deep copy
    }

    autosave(): void {
        if (this.family_member && ! this.family_member.equals(this.orig_family_member) ) {
            this.unsaved_family_member = true;
        } else {
            this.unsaved_family_member = false;
        }
    }

    saveFamilyMember(): void {
        this.restService.updateFamilyMember(this.family_member);
        this.setFamilyMember(this.family_member);
        this.unsaved_family_member = false;
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
    child: Child;
    private orig_family_member: FamilyMember;
    private unsaved_family_member: boolean;
}
