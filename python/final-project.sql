-- 1. Database structure
-- What are the primary keys in the individual tables?
-- odpoveď:
-- DIAGRAM -> v diagrame sú primárne kľúče označené žltou / zlatou farbou a sú v podnej časti tabuľky
-- DDL -> tu sú primárne kľúče ako prvé a sú označené ako primary key

-- What relationships do particular pairs of tables have?


-- 2. History of granted loans
select
    year(date) as year,
    quarter(date) as quarter,
    month(date) as month,

    sum(amount) as total_amount,
    avg(amount) as average_amount,
    count(amount) as total_loans
from loan
group by year, quarter, month
order by year;

select
    sum(amount) as total_amount,
    avg(amount) as average_amount,
    count(amount) as total_loans
from loan;

-- 3. Loan status
-- repaid 606 (A + C)
-- unpaid 76 (B + D)
select
    status,
    count(*) as pocet
from loan
group by status
order by status;

-- 4. Analysis of accounts
-- vychádza mi, že všetci mali iba 1 pôžičku takže avg = sum
with cte_loans as (
    select
        account_id,
        count(loan_id) as nr_of_given_loans,
        sum(amount) as amount_of_given_loans,
        avg(amount) as avg_loan_amount
    from loan
    where status in ('A', 'C')
    group by account_id

)

select *,
    dense_rank() over (order by nr_of_given_loans desc) as ranking_sumy,
    dense_rank() over (order by amount_of_given_loans desc) as ranking_sumy,
    dense_rank() over (order by avg_loan_amount desc) as ranking_sumy
from cte_loans;

-- 5. Fully paid loans
select 
	gender,
	count(l.loan_id ) as total_qty_of_loans
from loan l
join account a on l.account_id = a.account_id
join disp d on a.account_id = d.account_id
join client c on d.client_id = c.client_id
where l.status in ('A', 'C')
	and d.type = 'OWNER'
group by c.gender ;

-- 6. Client analysis - part 1

drop temporary table if exists tmp_part_1;
create temporary table tmp_part_1 as (
    select
        gender,
        count(amount) as number_of_loans,
        2025 - year(c.birth_date) as age
    from loan l
    join account a on l.account_id = a.account_id
    join disp d  on a.account_id = d.account_id
    join client c on d.client_id = c.client_id
    where true
        and status in ('A', 'C')
        and type = 'OWNER'
    group by gender, age);

-- Who has more repaid loans - women or men?: ženy
select
    gender,
    sum(number_of_loans) as pocet_poziciek
from tmp_part_1
group by gender;

-- What is the average age of the borrower divided by gender?: M -> 67,5 / F -> 65,5
select
    gender,
    avg(age) as avg_age
from tmp_part_1
group by gender;

-- 7. Client analysis - part 2
-- vysledok pri kontrole som mal rovnaký ALE kód z LMS mal trošku iné čísla
-- napr nr_of_customers / nr_of_loans mi podla kodu z LMS vychádzal na 73 a moj kod dáva 77
drop temporary table if exists tmp_part_2;
create temporary table tmp_part_2 as (
    select
        dt.district_id,
        count(c.client_id) as nr_of_customers,
        sum(amount) as total_amount,
        count(amount) as nr_of_loans
    from loan l
    join account a on l.account_id = a.account_id
    join disp d  on a.account_id = d.account_id
    join client c on d.client_id = c.client_id
    join district dt on a.district_id = dt.district_id
    where true
        and status in ('A', 'C')
        and type = 'OWNER'
    group by dt.district_id);

-- which area has the most clients?: dsitrict_id 1
select *
from tmp_part_2
order by nr_of_customers desc
limit 1;

-- in which area the highest number of loans was paid?: dsitrict_id 1
select *
from tmp_part_2
order by nr_of_loans desc
limit 1;

-- in which area the highest amount of loans was paid?: dsitrict_id 1
select *
from tmp_part_2
order by total_amount desc
limit 1;

-- 8. Client analysis - part 3
with cte as (
    select
        dt.district_id,
        count(c.client_id) as nr_of_customers,
        sum(amount) as total_amount,
        count(amount) as nr_of_loans
    from loan l
    join account a on l.account_id = a.account_id
    join disp d  on a.account_id = d.account_id
    join client c on d.client_id = c.client_id
    join district dt on a.district_id = dt.district_id
    where true
        and status in ('A', 'C')
        and type = 'OWNER'
    group by dt.district_id)

select *,
       total_amount / sum(total_amount) over() * 100 as share
from cte;

-- 9. Selection - part 1
-- z predchádzajúcej analýzy viem, že klienti, ktorých mám k dispozícií majú všetci iba 1 pôžičku
-- tabuľka bude prázdna
-- idem skúsiť ale aspoň balance + narodenie
with cte as (
	select
	    c.client_id ,
	    c.birth_date,
	    YEAR(c.birth_date) as year_of_birth,
	    sum(amount - payments) as client_balance,
	    count(loan_id) as loans_amount
	from loan l
	join account a on l.account_id = a.account_id
	join disp d  on a.account_id = d.account_id
	join client c on d.client_id = c.client_id
	join district dt on a.district_id = dt.district_id
	where true
	    and status in ('A', 'C')
	    and type = 'OWNER'
	group by c.client_id, c.birth_date)

select *
from cte
where year_of_birth > 1990
	and loans_amount >= 5
	and client_balance > 1000;

-- 10. Selection - part 2
-- žiadny z klientov nie je starší ako 1990
-- tak isto už z predchádzajúcich výsledkov viem, že na každeho klienta v datasete pripradá iba 1 pôžička
with cte as (
	select
	    c.client_id ,
	    c.birth_date,
	    YEAR(c.birth_date) as year_of_birth,
	    sum(amount - payments) as client_balance,
	    count(loan_id) as loans_amount
	from loan l
	join account a on l.account_id = a.account_id
	join disp d  on a.account_id = d.account_id
	join client c on d.client_id = c.client_id
	join district dt on a.district_id = dt.district_id
	where true
	    and status in ('A', 'C')
	    and type = 'OWNER'
	group by c.client_id, c.birth_date)

select *
from cte
where year_of_birth > 1990;

-- 11. Expiring cards
drop procedure tg_expirated_cards;
delimiter //
create procedure tg_expirated_cards(in in_date date)
begin
    with cte as (
        select
            c.client_id,
            card_id,
            cast(issued as date),
            A3,
            date_add(issued, interval 3 year) as expiration_date
        from card
        join disp d on card.disp_id = d.disp_id
        join client c on d.client_id = c.client_id
        join district as dt on c.district_id = dt.district_id),

    cte_2 as (
    select *,
           date_add(expiration_date, interval -7 day) as ready_to_contact
    from cte)

    select *
    from cte_2
    where ready_to_contact = in_date;
end; //

call tg_expirated_cards('2001-08-02');
