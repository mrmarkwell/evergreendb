import { Component, OnChanges, OnInit, Input } from '@angular/core';

import { Child } from '../../child';
import { Interaction } from '../../interaction';
import { RestService } from '../../rest.service';

@Component({
    selector: 'interactions-tab',
    templateUrl: './interactions-tab.component.html',
    styleUrls: ['./interactions-tab.component.scss']
})
export class InteractionsTabComponent implements OnInit, OnChanges {
    @Input() child_id: number;
    private child: Child;
    private interactions: Interaction[];
    private expanded_interaction: Interaction;
    constructor(
        private restService: RestService
    ) {}

    ngOnInit(): void {
        this.getChild();
        this.getInteractions();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }
    ngOnChanges(): void {
        this.getChild();
        this.getInteractions();
    }
    getChild(): void {
        this.restService.getChild(this.child_id).then(child => this.child = child);
    }
    getInteractions(): Promise<Interaction[]> {
        return this.restService.getInteractions(this.child_id)
            .then(interactions => {
                for (let interaction of interactions) {
                    interaction.interaction_date_object = this.restService.getDateFromString(interaction.interaction_date);
                }
                return this.interactions = interactions;
            });
    }
    selectInteraction(id: number): void {
        this.expanded_interaction = this.interactions.find(interaction => interaction.id === id);
    }
    isSelected(interaction): boolean {
        return this.expanded_interaction && interaction.id === this.expanded_interaction.id;
    }
    createInteraction() : void {
        let interaction = new Interaction();
        interaction.interaction_type = 'To Do';
        interaction.child_id = this.child_id;
        interaction.interaction_date = '2017-09-04';
        this.restService.addInteraction(interaction).then(new_interaction => {
            this.getInteractions().then(interactions => this.selectInteraction(new_interaction.id));
        });
    }
}
