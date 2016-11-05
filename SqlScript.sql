update amgen.studentData set password='temp' where Username = ('v.patanjali@gmail.com');

select * from amgen.References;
select * from amgen.studentData;
select * from amgen.Mentors;
select * from amgen.Courses;


update amgen.studentData set Transcript=null where Username in ('shivani','tulika')
update amgen.studentData set UserType='Student' where Username in ('shivani','tulika')
update amgen.studentData set ApplicationStatus='IncompleteApplication' where Username ='pv2270@columbia.edu'
update amgen.studentData set ApplicationStatus='UnderReview' where Username in ('shivani','tulika')
update amgen.studentData set ApplicationStatus='ReferencesRequired1' where Username in ('sg3296@columbia.edu')


drop table amgen.Courses;
drop table amgen.References;
drop table amgen.studentData;