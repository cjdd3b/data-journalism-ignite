select category, count(*)
from (select blog_extraextra.id as eeid
from blog_extraextra
inner join blog_extraextra_extraextra_category on blog_extraextra."id" = blog_extraextra_extraextra_category.extraextra_id
inner join blog_extraextracategory on blog_extraextracategory."id" = blog_extraextra_extraextra_category.extraextracategory_id
where blog_extraextracategory.category = 'CAR') as carposts
inner join blog_extraextra_extraextra_category on blog_extraextra_extraextra_category.extraextra_id = carposts.eeid
inner join blog_extraextracategory on blog_extraextracategory."id" = blog_extraextra_extraextra_category.extraextracategory_id
group by category
order by 2 desc