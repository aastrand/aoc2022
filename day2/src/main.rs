use aocrust::io::lines_from_file;

fn shape_to_pos(shape: &str) -> usize {
    match shape {
        "A" => 0,
        "B" => 1,
        "C" => 2,
        "X" => 0,
        "Y" => 1,
        "Z" => 2,
        _ => {
            panic!("Unexpected input");
        }
    }
}

fn solve1(filename: &str) -> u64 {
    let input = &lines_from_file(filename);
    let pairs: Vec<Vec<usize>> = input
        .iter()
        .map(|s| s.split(" ").map(|p| shape_to_pos(p)).collect())
        .collect();

    let outcomes = vec![
        vec![3, 0, 6], // rr, rp, rs
        vec![6, 3, 0], // pr, pp, ps
        vec![0, 6, 3], // sr, sp, ss
    ];

    pairs
        .iter()
        // match point = shape + 1 + win/lose/draw from outcomes
        .map(|p| p[1] + 1 + outcomes[p[1] as usize][p[0] as usize])
        .sum::<usize>() as u64
}

fn solve2(filename: &str) -> u64 {
    let input = &lines_from_file(filename);
    let pairs: Vec<Vec<usize>> = input
        .iter()
        .map(|s| s.split(" ").map(|p| shape_to_pos(p)).collect())
        .collect();

    let inverse = vec![
        vec![2, 0, 1], // lose
        vec![0, 1, 2], // draw
        vec![1, 2, 0], // win,
    ];

    pairs
        .iter()
        // match point = win/lose/draw pre-determined + shape for outcome + 1
        .map(|p| (p[1] * 3) + inverse[p[1] as usize][p[0] as usize] + 1)
        .sum::<usize>() as u64
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
        assert_eq!(solve1("example.txt"), 15);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve2("example.txt"), 12);
    }
}
