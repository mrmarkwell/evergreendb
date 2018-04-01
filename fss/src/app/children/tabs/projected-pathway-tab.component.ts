import { Component, OnChanges, OnInit, Input } from '@angular/core';
import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';

import { Child } from '../../child';
import { ProjectedPathway } from '../../projected-pathway';
import { RestService } from '../../rest.service';

@Component({
    selector: 'projected-pathway-tab',
    templateUrl: './projected-pathway-tab.component.html',
    styleUrls: ['./projected-pathway-tab.component.scss']
})


export class ProjectedPathwayTabComponent implements OnInit, OnChanges {
    child: Child;
    projectedPathways: ProjectedPathway[];
    private orig_projected_pathways: ProjectedPathway[];
    private changed_projected_pathways: ProjectedPathway[];
    private unsaved: boolean;

    @Input() child_id: number;

    constructor(
        private restService: RestService
    ) { }

    ngOnInit(): void {
        this.getChild();
        this.getProjectedPathways();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
        setInterval(()=>this.autosave(), this.restService.settings.save_notify_interval);
    }

    ngOnChanges(): void {
        this.getChild();
        this.getProjectedPathways();
    }

    autosave(): void {
        let save_needed = false;
        this.projectedPathways.forEach((item,index) => {
            item.pathway_completion_date = this.restService.getStringFromDate(item.pathway_completion_date_object);
            if (! item.equals(this.orig_projected_pathways[index])) {
                save_needed = true;
            }
        })
        if (save_needed) {
            let idle = true;
            this.projectedPathways.forEach((item,index) => {
                item.pathway_completion_date = this.restService.getStringFromDate(item.pathway_completion_date_object);
                if (! item.equals(this.changed_projected_pathways[index])) {
                    idle = false;
                }
            })
            if (idle && this.unsaved) {
                //this.save(); // Don't autosave, the focus loss is too distracting.
            } else {
                this.unsaved = true;
                this.changed_projected_pathways = this.projectedPathways.map(pathway => {
                    return Object.assign(Object.create(pathway), pathway); // deep copy
                })
            }
        } else {
            this.unsaved = false;
        }
    }

save(): void {
        this.unsaved = false;
        for (let pathway of this.projectedPathways) {
            // Update the pathway completion date with the object that is tied to the datepicker.
            pathway.pathway_completion_date = this.restService.getStringFromDate(pathway.pathway_completion_date_object);
            this.restService.updateProjectedPathway(pathway);
        }
    }

    delete(pathway_id: number): void {
        if (confirm("Are you sure you want to delete this step?")) {
            this.restService.deleteProjectedPathway(pathway_id);
        }
    }

    addNewStep(): void {
        if (this.unsaved) this.save();
        let next_step = 1;
        let latest_pathway = this.projectedPathways.slice(-1)[0];
        if (latest_pathway) {
            next_step = latest_pathway.pathway_step_number + 1;
        }
        let new_pathway = new ProjectedPathway({
            "pathway_step_number": next_step,
            "child_id": this.child_id
        });
        this.restService.addProjectedPathway(new_pathway);
    }

    getChild(): void {
        this.restService.getChild(this.child_id).then(child => this.child = child);
    }
    getProjectedPathways(): void {
        this.restService.getProjectedPathway(this.child_id).then(pathways => {
            // Sort them by step number
            pathways.sort(
                function (a, b) {
                    return (a.pathway_step_number > b.pathway_step_number) ? 1
                        : ((a.pathway_step_number < b.pathway_step_number) ? -1
                            : 0);
                }
            );
            this.projectedPathways = pathways;
            let step_number = 1;
            let active_found = false;
            for (let pathway of this.projectedPathways) {
                // Reset the pathway numbers to increment starting at 1.
                // This ensures that the steps are numbered appropriately even if steps are deleted.
                pathway.pathway_step_number = step_number++;

                // Make a Date object for the pathway_completion_date. Datepicker wants to be tied to a date object.
                if (pathway.pathway_completion_date) {
                    let theDate = this.restService.getDateFromString(pathway.pathway_completion_date);

                    pathway.pathway_completion_date_object = theDate;
                }
                else {
                    // If this is the first pathway step with no pathway_completion_date_object then mark it as active
                    if (!active_found) {
                        active_found = true
                        pathway.pathway_is_active = true
                    }
                    pathway.pathway_completion_date_object = null;
                }
                pathway.pathway_completion_date = this.restService.getStringFromDate(pathway.pathway_completion_date_object)
            }
            this.orig_projected_pathways = this.projectedPathways.map(pathway => {
                return Object.assign(Object.create(pathway), pathway); // deep copy
            })
            this.changed_projected_pathways = this.projectedPathways.map(pathway => {
                return Object.assign(Object.create(pathway), pathway); // deep copy
            })
        });
    }

}
