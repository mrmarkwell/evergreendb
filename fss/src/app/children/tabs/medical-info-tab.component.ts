import { Component, OnChanges, OnInit, Input } from '@angular/core';

import { Child } from '../../child';
import { RestService } from '../../rest.service';

@Component({
    selector: 'medical-info-tab',
    styleUrls: ['./medical-info-tab.component.css'],
    templateUrl: './medical-info-tab.component.html'
})
export class MedicalTabComponent implements OnInit, OnChanges {
    private child: Child;
    private conditions: String[];
    constructor(
        private restService: RestService
    ) {}
	ngOnInit(): void {
        this.getChild();
        this.getMedicalConditions();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }
    ngOnChanges(): void {
        this.getChild();
    }
    save(): void {
        this.restService.updateChild(this.child)
    }
    getChild(): void {
        this.restService.getChild(this.child_id).then(child => this.child = child);
    }
    getMedicalConditions(): void {
        this.restService.getEnum('fss_medical_condition').then(conditions => this.conditions = conditions)
    }
    @Input() child_id: number;
}
