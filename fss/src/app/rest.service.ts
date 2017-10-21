import { Injectable, EventEmitter } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Child } from './child';
import { ChildPhoto } from './child-photo'
import { Interaction } from './interaction';
import { FamilyMember } from './family-member';
import { ProjectedPathway } from './projected-pathway';

@Injectable()
export class RestService {
	changeEmitter: EventEmitter<any> = new EventEmitter();
	constructor(private http: Http) {}

	emit(): void { this.changeEmitter.emit(); }

	// Generic functions
	getEntity(type: string, query?:string): Promise<any> {
		let url = `${this.evergreenUrl}/entity/${type}`;
		if (query) {url = url + '?' + query};
		return this.http.get(url)
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}
	addEntity(type: string, entity: any): Promise<any> {
		let url = `${this.evergreenUrl}/entity/${type}`;
		return this.http.post(url, JSON.stringify(entity), {headers: this.headers})
			.toPromise().then(res => { this.emit(); return res.json() })
			.catch(this.handleError);
	}
	updateEntity(type:string, entity: any): Promise<any> {
		const url = `${this.evergreenUrl}/entity/${type}?id=${entity.id}`;
		return this.http.put(url, JSON.stringify(entity), {headers: this.headers})
			.toPromise().then(res => { this.emit(); return res.json() })
			.catch(this.handleError);
	}
	deleteEntity(type: string, id: number): Promise<void> {
		const url = `${this.evergreenUrl}/entity/${type}?id=${id}`;
		return this.http.delete(url, {headers: this.headers})
			.toPromise().then( () => { this.emit(); return null }).catch(this.handleError);
	}

	getEnum(field: string): Promise<string[]> {
		let url = `${this.evergreenUrl}/enum/${field}`;
		return this.http.get(url)
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}

    // TODO: Better error handling of bad backend responses.
	// Child functions
	getChildren(refresh: boolean = true): Promise<Child[]> {
		return this.getEntity('fss_child').then( results => results.map(child => new Child(child)));
	}
	getChild(child_id: number): Promise<Child> {
        return this.getEntity('fss_child', `id=${child_id}`).then(child => new Child(child[0]));
	}
	addChild(child: Child): Promise<Child> {
		return this.addEntity('fss_child', child).then(results => results as Child);
	}
	updateChild(child: Child): Promise<Child> {
		return this.updateEntity('fss_child', child).then(results => results as Child);
	}
	deleteChild(id: number): Promise<void> {
		return this.deleteEntity('fss_child', id);
	}

	// Interactions, family members, and projected pathways are all pretty much the same except the url and return class
	getInteractions(child_id: number): Promise<Interaction[]> {
		return this.getEntity('fss_interaction',`child_id=${child_id}`).then( results => results as Interaction[] );
	}
	addInteraction(interaction: Interaction): Promise<Interaction> {
		return this.addEntity('fss_interaction', interaction).then(results => results as Interaction);
	}
	updateInteraction(interaction: Interaction): Promise<Interaction> {
		return this.updateEntity('fss_interaction', interaction).then(results => results as Interaction);
	}
	deleteInteraction(id: number): Promise<void> {
		return this.deleteEntity('fss_interaction',id);
	}

	getFamilyMembers(child_id: number): Promise<FamilyMember[]> {
		return this.getEntity('fss_family_member',`child_id=${child_id}`).then( results => results as FamilyMember[] );
	}
	addFamilyMember(family_member: FamilyMember): Promise<FamilyMember> {
		return this.addEntity('fss_family_member', family_member).then(results => results as FamilyMember);
	}
	updateFamilyMember(family_member: FamilyMember): Promise<FamilyMember> {
		return this.updateEntity('fss_family_member', family_member).then(results => results as FamilyMember);
	}
	deleteFamilyMember(id: number): Promise<void> {
		return this.deleteEntity('fss_family_member',id);
	}

	getProjectedPathway(child_id: number): Promise<ProjectedPathway[]> {
		return this.getEntity('fss_projected_pathway',`child_id=${child_id}`).then( results => results as ProjectedPathway[] );
	}
	addProjectedPathway(projected_pathway: ProjectedPathway): Promise<ProjectedPathway> {
		return this.addEntity('fss_projected_pathway', projected_pathway).then(results => results as ProjectedPathway);
	}
	updateProjectedPathway(projected_pathway: ProjectedPathway): Promise<ProjectedPathway> {
		return this.updateEntity('fss_projected_pathway', projected_pathway).then(results => results as ProjectedPathway);
	}
	deleteProjectedPathway(id: number): Promise<void> {
		return this.deleteEntity('fss_projected_pathway',id);
	}

	// Utility function for creating Date objects from strings for binding to datepickers.
	getDateFromString(date_string: string): Date {
		if (date_string == null || date_string.length == 0) return null;
		return new Date(date_string.replace(/-/g, '\/').replace(/T.+/, ''));
	}	

	// Utility function for creating a string from a Date object.
	getStringFromDate(date_obj: Date): string {
		if (date_obj) {
			let day = date_obj.getDate();
			let month = date_obj.getMonth() + 1;
			let year = date_obj.getFullYear();
			let date_string = year + "-" + month + "-" + day;

			return date_string;
		}
		else {
			return "";
		}
	}

    // uploadChildPhoto(photo: File): Promise<any> {
	//     let url = `${this.evergreenUrl}/upload`;
    //    return this.http.post(url, JSON.stringify(photo), {headers: this.headers})
	// 		.toPromise().then(res => { this.emit(); return res.json() })
	// 		.catch(this.handleError); 
    // }

    getPhotoUploadUrl(): string {
        return this.evergreenUrl + "/upload";
    } 
	getChildPhotoUrl(id: number): string {
        return `${this.evergreenUrl}/static/photos/child${id}.jpeg`;
    }
    // tryGetChildPhoto(id: number): Promise<File> {
	// 	let url = this.getChildPhotoUrl(id); 
	// 	return this.http.get(url)
	// 		.toPromise()
	// 		.catch(error => null); 
	// } 



    private handleError(error: any): Promise<any> {
		console.error('An error occurred', error);
		return Promise.reject(error.message || error);
	}

    //File uploader needs the photo upload 

	private evergreenUrl = 'http://127.0.0.1:5000';
    // private evergreenUrl = "http://ec2-54-193-44-138.us-west-1.compute.amazonaws.com";
	private headers = new Headers({'Content-Type': 'application/json'});
}
