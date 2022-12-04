use aocrust::io::lines_from_file;

fn test_pairs<F>(input: &Vec<String>, f: F) -> u64
where
    F: Fn(&Vec<u64>, &Vec<u64>) -> bool,
{
    let mut sum = 0;
    for p in input {
        let pairs = p.split(",").collect::<Vec<&str>>();
        let p1 = pairs[0]
            .split("-")
            .map(|s| s.parse::<u64>().unwrap())
            .collect::<Vec<u64>>();
        let p2 = pairs[1]
            .split("-")
            .map(|s| s.parse::<u64>().unwrap())
            .collect::<Vec<u64>>();

        if f(&p1, &p2) {
            sum += 1;
        }
    }

    sum
}

fn solve1(filename: &str) -> u64 {
    test_pairs(
        &lines_from_file(filename),
        |p1: &Vec<u64>, p2: &Vec<u64>| {
            p1[0] <= p2[0] && p1[1] >= p2[1] || (p2[0] <= p1[0] && p2[1] >= p1[1])
        },
    )
}

fn solve2(filename: &str) -> u64 {
    test_pairs(
        &lines_from_file(filename),
        |p1: &Vec<u64>, p2: &Vec<u64>| {
            (p1[0] <= p2[0] && p1[0] >= p2[1])
                || (p1[1] >= p2[0] && p1[1] <= p2[1])
                || (p2[0] <= p1[0] && p2[0] >= p1[1])
                || (p2[1] >= p1[0] && p2[1] <= p1[1])
        },
    )
}

fn main() {
    println!("{}", solve1("input.txt"));
    println!("{}", solve2("input.txt"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(solve1("example.txt"), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve2("example.txt"), 4);
    }
}
