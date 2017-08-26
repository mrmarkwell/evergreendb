import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { ParamMap } from '@angular/router';

import { FamilyMember } from '../../family-member';
import { RestService } from '../../rest.service';

@Component({
    selector: 'family-list',
    templateUrl: './family-list.component.html',
    styleUrls: ['./family-list.component.css']
})
export class FamilyListComponent implements OnInit {
    constructor(
        private restService: RestService
    ) {}
    ngOnInit(): void {
        this.restService.getFamilyMembers(1).then(family_members => { console.log(family_members); this.family_members =  family_members });
    }
    onSelect(selected: FamilyMember) : void {
      this.selected_family_member = selected;
      this.notifySelected.emit(selected);
    }
    private family_members: FamilyMember[];
    private selected_family_member: FamilyMember;
    @Output() notifySelected = new EventEmitter<FamilyMember>();
}
