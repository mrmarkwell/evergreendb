import {Injectable} from '@angular/core';
import {Http, Headers} from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Child } from './child';
import { Interaction } from './interaction';
import { FamilyMember } from './family-member';
import { ProjectedPathway } from './projected-pathway';

@Injectable()
export class RestService {
	constructor(private http: Http) {}

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
			.toPromise().then(res => res.json().data)
			.catch(this.handleError);
	}
	updateEntity(type:string, entity: any): Promise<any> {
		const url = `${this.evergreenUrl}/entity/${type}?id=${entity.id}`;
		return this.http.put(url, JSON.stringify(entity), {headers: this.headers})
			.toPromise().then(res => res.json().data)
			.catch(this.handleError);
	}
	deleteEntity(type: string, id: number): Promise<void> {
		const url = `${this.evergreenUrl}/entity/${type}?id=${id}`;
		return this.http.delete(url, {headers: this.headers})
			.toPromise().then( () => null ).catch(this.handleError);
	}

	getEnum(field: string): Promise<string[]> {
		let url = `${this.evergreenUrl}/enum/${field}`;
		return this.http.get(url)
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}

	// Child functions
	getChildren(refresh: boolean = true): Promise<Child[]> {
		if (refresh || !this.childrenCache) {
			return this.getEntity('fss_child').then( results => this.childrenCache = results as Child[] );
		} else {
			return new Promise( (resolve,reject) => resolve(this.childrenCache) );
		}
	}
	getChild(child_id: number): Promise<Child> {
		return this.getChildren(false).then(children => children.find(child => child.id === child_id))
	}
	addChild(child: Child): Promise<Child> {
		return this.addEntity('fss_child', child).then(results => results as Child);
	}
	updateChild(child: Child): Promise<Child> {
		return this.updateEntity('fss_child', child).then(results => results as Child);
	}
	deleteChild(id: number): Promise<void> {
		return this.deleteEntity('fss_child',id);
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

	private handleError(error: any): Promise<any> {
		console.error('An error occurred', error);
		return Promise.reject(error.message || error);
	}

	private evergreenUrl = 'http://127.0.0.1:5000';
	private headers = new Headers({'Content-Type': 'application/json'});
	private childrenCache: Child[];
}
