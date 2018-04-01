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
        setInterval(()=>this.autosave(), this.restService.settings.save_notify_interval);
    }

    ngOnChanges(changes: SimpleChanges): void {
        if ("child_id" in changes) {
            this.family_member = null;
            this.restService.getChild(this.child_id).then(child => {
                this.setChild(child);
            });
        }
    }

    onSelect(family_member: FamilyMember): void {
        this.setFamilyMember(family_member);
    }

    setFamilyMember(family_member: FamilyMember): void {
      this.family_member = family_member;
      this.orig_family_member = Object.assign(Object.create(family_member), family_member); // deep copy
      this.changed_family_member = Object.assign(Object.create(family_member), family_member); // deep copy
    }

    setChild(child: Child): void {
        this.child = child;
        this.orig_child = Object.assign(Object.create(child), child); // deep copy
        this.changed_child = Object.assign(Object.create(child), child); // deep copy
    }

    autosave(): void {
        if ( ! this.child.equals(this.orig_child) ) {
            if (! this.child.equals(this.changed_child)) {
                this.unsaved_child = true;
                this.changed_child = Object.assign(Object.create(this.child), this.child); // deep copy
            } else {
                //this.saveChild();
            }
        } else {
            this.unsaved_child = false;
        }
        if (this.family_member && ! this.family_member.equals(this.orig_family_member) ) {
            if (! this.family_member.equals(this.changed_family_member)) {
                this.unsaved_family_member = true;
                this.changed_family_member = Object.assign(Object.create(this.family_member), this.family_member); // deep copy
            } else {
                //this.saveFamilyMember();
            }
        } else {
            this.unsaved_family_member = false;
        }
    }

    saveFamilyMember(): void {
        this.restService.updateFamilyMember(this.family_member);
        this.setFamilyMember(this.family_member);
        this.unsaved_family_member = false;
    }

    saveChild(): void {
        this.restService.updateChild(this.child);
        this.setChild(this.child);
        this.unsaved_child = false;
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
    private orig_child: Child;
    private changed_family_member: FamilyMember;
    private changed_child: Child;
    private unsaved_family_member: boolean;
    private unsaved_child: boolean;
}
