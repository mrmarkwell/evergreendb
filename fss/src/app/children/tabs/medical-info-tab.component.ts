import { Component, OnChanges, OnInit, Input } from '@angular/core';

import { Child } from '../../child';
import { RestService } from '../../rest.service';

@Component({
    selector: 'medical-info-tab',
    styleUrls: ['./medical-info-tab.component.scss'],
    templateUrl: './medical-info-tab.component.html'
})
export class MedicalTabComponent implements OnInit, OnChanges {
    child: Child;
    private orig_child: Child;
    private conditions: String[];
    constructor(
        private restService: RestService
    ) {}
    ngOnInit(): void {
        this.getChild();
        this.getMedicalConditions();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
        setInterval(()=>this.autosave(), this.restService.autosave_frequency);
    }
    ngOnChanges(): void {
        this.getChild();
    }
    autosave(): void {
        if ( ! this.child.equals(this.orig_child) ) {
            this.save();
        }
    }
    save(): void {
        this.restService.updateChild(this.child)
    }
    getChild(): void {
        this.restService.getChild(this.child_id).then(child => {
            this.child = child;
            this.orig_child = Object.assign(Object.create(child), child);
        });
    }
    getMedicalConditions(): void {
        this.restService.getEnum('fss_medical_condition').then(conditions => this.conditions = conditions)
    }
    @Input() child_id: number;
}
