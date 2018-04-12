import * as moment from 'moment';

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
    interactions: Interaction[];
    expanded_interaction: Interaction;
    constructor(
        private restService: RestService
    ) {}

    ngOnInit(): void {
        this.getInteractions();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }
    ngOnChanges(): void {
        if (this.child_id != null
            && this.expanded_interaction != null
            && this.child_id !== this.expanded_interaction.child_id) {
                this.expanded_interaction = null;
            }
        this.getInteractions();
    }
    hasAttachments(id: number) : Promise<boolean> {
        return this.restService.getInteractionFiles(id).then(files => files['filenames'].length != 0);
    }
    getInteractions(): Promise<Interaction[]> {
        return this.restService.getInteractions(this.child_id)
            .then(interactions => {
                for (let interaction of interactions) {
                    interaction.interaction_date_object = this.restService.getDateFromString(interaction.interaction_date);
                    this.hasAttachments(interaction.id).then(result => interaction.has_attachments = result);
                }
                interactions.sort((a,b) => b.interaction_date_object.valueOf() - a.interaction_date_object.valueOf())
                return this.interactions = interactions;
            });
    }
    handleNotification(type: string): void {
        if (type == "hidden") {
            this.expanded_interaction = null;
          } else if (type == "deleted")  {
            this.getInteractions();
          }
    }
    selectInteraction(id: number): void {
        this.expanded_interaction = this.interactions.find(interaction => interaction.id === id);
    }
    isSelected(interaction): boolean {
        return this.expanded_interaction && interaction.id === this.expanded_interaction.id;
    }
    isFuture(interaction): boolean {
        let d = moment();
        return interaction.interaction_date_object >= d;
    }
    createInteraction() : void {
        let interaction = new Interaction({
            "interaction_type": "To Do",
            "child_id": this.child_id,
            "interaction_date": this.restService.getStringFromDate(moment())
        });
        this.restService.addInteraction(interaction).then(new_interaction => {
            this.getInteractions().then(interactions => this.selectInteraction(new_interaction.id));
        });
    }
}
