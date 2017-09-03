import { Component, OnInit, OnChanges, EventEmitter, Output, Input } from '@angular/core';
import { ParamMap } from '@angular/router';

import { FamilyMember } from '../../family-member';
import { RestService } from '../../rest.service';

@Component({
    selector: 'family-list',
    templateUrl: './family-list.component.html',
    styleUrls: ['./family-list.component.css']
})
export class FamilyListComponent implements OnInit, OnChanges {
    constructor(
      private restService: RestService
    ) {}
    ngOnInit(): void {
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }
    ngOnChanges(): void {
      this.getFamilyMembers();
      this.notifySelected.emit(null);
    }
    isSelected(family_member): boolean {
      // Object equality doesn't work in js/ts. It just checks if instances are the same not contents are equal
      return this.selected_family_member && family_member.id === this.selected_family_member.id;
    }
    onSelect(selected: FamilyMember) : void {
      this.selected_family_member = selected;
      this.notifySelected.emit(selected);
    }
    createFamilyMember() : void {
        let family_member = new FamilyMember();
        family_member.relationship = "Family Member";
        family_member.child_id = this.child_id;
        this.restService.addFamilyMember(family_member).then(new_family_member => {
            this.getFamilyMembers();
            this.onSelect(new_family_member);
        });
    }
    getFamilyMembers(): void {
        this.restService.getFamilyMembers(this.child_id)
            .then(family_members => this.family_members = family_members );
    }
    @Input() child_id: number;
    @Output() notifySelected = new EventEmitter<FamilyMember>();
    private family_members: FamilyMember[];
    private selected_family_member: FamilyMember;
}
