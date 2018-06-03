export class FamilyMember {
  constructor(jsondata){
      for (let attr in jsondata) {
          this[attr] = jsondata[attr];
      }
  }

  equals(fm2: FamilyMember): boolean {
      return this.id == fm2.id
          && this.child_id == fm2.child_id
          && this.family_member_address == fm2.family_member_address
          && this.family_member_email == fm2.family_member_email
          && this.family_member_is_primary == fm2.family_member_is_primary
          && this.family_member_name == fm2.family_member_name
          && this.family_member_notes == fm2.family_member_notes
          && this.family_member_phone == fm2.family_member_phone
          && this.family_member_wechat == fm2.family_member_wechat
          && this.relationship == fm2.relationship
    }

    id: number;
    child_id: number;
    family_member_address: string;
    family_member_email: string;
    family_member_is_primary: boolean;
    family_member_name: string;
    family_member_notes: string;
    family_member_phone: string;
    family_member_wechat: string;
    relationship: string;
}
